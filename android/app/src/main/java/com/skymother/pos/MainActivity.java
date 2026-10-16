package com.skymother.pos;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.hardware.usb.UsbConstants;
import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbDeviceConnection;
import android.hardware.usb.UsbEndpoint;
import android.hardware.usb.UsbInterface;
import android.hardware.usb.UsbManager;
import android.net.Uri;
import android.os.Bundle;
import android.util.Base64;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends Activity {
    private WebView webView;
    private SharedPreferences prefs;
    private static final UUID SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        setContentView(webView);

        prefs = getSharedPreferences("SkyMotherPOS", MODE_PRIVATE);
        String serverUrl = prefs.getString("server_url", "http://localhost:8080");

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);

        // Native Printer JavaScript Bridge
        webView.addJavascriptInterface(new POSPrinterBridge(), "NativePrinter");

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return handleUri(request.getUrl());
            }

            @SuppressWarnings("deprecation")
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return handleUri(Uri.parse(url));
            }

            private boolean handleUri(Uri uri) {
                String scheme = uri.getScheme();
                if (scheme != null && !scheme.startsWith("http")) {
                    try {
                        Intent intent = scheme.equals("intent")
                                ? Intent.parseUri(uri.toString(), Intent.URI_INTENT_SCHEME)
                                : new Intent(Intent.ACTION_VIEW, uri);
                        startActivity(intent);
                        return true;
                    } catch (Exception e) {
                        Toast.makeText(MainActivity.this, "Printer သို့ ချိတ်ဆက်၍မရပါ", Toast.LENGTH_SHORT).show();
                        return true;
                    }
                }
                return false;
            }

            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                if (failingUrl != null && failingUrl.startsWith("http")) {
                    showConfigDialog();
                }
            }
        });

        webView.setOnLongClickListener(v -> {
            showConfigDialog();
            return true;
        });

        webView.loadUrl(serverUrl);
    }

    public class POSPrinterBridge {
        @JavascriptInterface
        public boolean isNative() {
            return true;
        }

        @JavascriptInterface
        public String getBluetoothDevices() {
            JSONArray arr = new JSONArray();
            try {
                BluetoothAdapter adapter = BluetoothAdapter.getDefaultAdapter();
                if (adapter != null && adapter.isEnabled()) {
                    @SuppressLint("MissingPermission") Set<BluetoothDevice> paired = adapter.getBondedDevices();
                    for (BluetoothDevice d : paired) {
                        JSONObject obj = new JSONObject();
                        @SuppressLint("MissingPermission") String name = d.getName();
                        obj.put("name", name != null ? name : "Unknown");
                        obj.put("address", d.getAddress());
                        arr.put(obj);
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
            return arr.toString();
        }

        @JavascriptInterface
        public void printBluetooth(String macAddress, String textBase64) {
            new Thread(() -> {
                try {
                    byte[] data = Base64.decode(textBase64, Base64.DEFAULT);
                    BluetoothAdapter adapter = BluetoothAdapter.getDefaultAdapter();
                    if (adapter == null) throw new Exception("Bluetooth မရှိပါ");
                    BluetoothDevice device = adapter.getRemoteDevice(macAddress);
                    @SuppressLint("MissingPermission") BluetoothSocket socket = device.createRfcommSocketToServiceRecord(SPP_UUID);
                    adapter.cancelDiscovery();
                    socket.connect();
                    OutputStream os = socket.getOutputStream();
                    os.write(data);
                    os.flush();
                    Thread.sleep(500);
                    socket.close();
                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "Bluetooth ပရင့် ထုတ်ပြီးပါပြီ", Toast.LENGTH_SHORT).show());
                } catch (Exception e) {
                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "Bluetooth Print မအောင်မြင်ပါ: " + e.getMessage(), Toast.LENGTH_LONG).show());
                }
            }).start();
        }

        @JavascriptInterface
        public void printUsb(String textBase64) {
            new Thread(() -> {
                try {
                    byte[] data = Base64.decode(textBase64, Base64.DEFAULT);
                    UsbManager manager = (UsbManager) getSystemService(Context.USB_SERVICE);
                    HashMap<String, UsbDevice> list = manager.getDeviceList();
                    UsbDevice printer = null;
                    UsbInterface pIntf = null;
                    UsbEndpoint pEndp = null;

                    for (UsbDevice dev : list.values()) {
                        for (int i = 0; i < dev.getInterfaceCount(); i++) {
                            UsbInterface intf = dev.getInterface(i);
                            if (intf.getInterfaceClass() == UsbConstants.USB_CLASS_PRINTER || dev.getInterfaceCount() == 1) {
                                for (int j = 0; j < intf.getEndpointCount(); j++) {
                                    UsbEndpoint ep = intf.getEndpoint(j);
                                    if (ep.getDirection() == UsbConstants.USB_DIR_OUT) {
                                        printer = dev;
                                        pIntf = intf;
                                        pEndp = ep;
                                        break;
                                    }
                                }
                            }
                            if (printer != null) break;
                        }
                        if (printer != null) break;
                    }

                    if (printer == null) throw new Exception("USB Printer ချိတ်ဆက်မထားပါ");

                    UsbDeviceConnection conn = manager.openDevice(printer);
                    if (conn == null) throw new Exception("USB ခွင့်ပြုချက် မရပါ");
                    conn.claimInterface(pIntf, true);
                    conn.bulkTransfer(pEndp, data, data.length, 5000);
                    conn.releaseInterface(pIntf);
                    conn.close();
                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "USB ပရင့် ထုတ်ပြီးပါပြီ", Toast.LENGTH_SHORT).show());
                } catch (Exception e) {
                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "USB Print မအောင်မြင်ပါ: " + e.getMessage(), Toast.LENGTH_LONG).show());
                }
            }).start();
        }
    }

    private void showConfigDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("POS Server ချိတ်ဆက်ရန် IP");
        final EditText input = new EditText(this);
        input.setHint("ဥပမာ - http://192.168.1.15:8080");
        input.setText(prefs.getString("server_url", "http://localhost:8080"));
        builder.setView(input);

        builder.setPositiveButton("ချိတ်မည်", (dialog, which) -> {
            String url = input.getText().toString().trim();
            if (!url.startsWith("http://") && !url.startsWith("https://")) {
                url = "http://" + url;
            }
            prefs.edit().putString("server_url", url).apply();
            webView.loadUrl(url);
        });
        builder.setNegativeButton("ပိတ်မည်", (dialog, which) -> dialog.cancel());
        builder.show();
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
