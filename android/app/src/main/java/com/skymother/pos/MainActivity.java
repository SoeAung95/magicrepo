package com.skymother.pos;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.hardware.usb.UsbConstants;
import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbDeviceConnection;
import android.hardware.usb.UsbEndpoint;
import android.hardware.usb.UsbInterface;
import android.hardware.usb.UsbManager;
import android.net.Uri;
import android.os.Build;
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
import java.util.HashMap;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends Activity {
    private WebView webView;
    private SharedPreferences prefs;
    private static final UUID SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    private static final String DEFAULT_PRINTER_MAC = "AB:0D:9E:AD:7F:9B";

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        setContentView(webView);

        // Android 12+ Bluetooth Runtime Permissions တောင်းဆိုခြင်း
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (checkSelfPermission(Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{
                        Manifest.permission.BLUETOOTH_CONNECT,
                        Manifest.permission.BLUETOOTH_SCAN
                }, 101);
            }
        }

        prefs = getSharedPreferences("SkyMotherPOS", MODE_PRIVATE);
        String serverUrl = prefs.getString("server_url", "http://localhost:8080");

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);

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
                        Toast.makeText(MainActivity.this, "Printer App သို့ ပို့၍မရပါ", Toast.LENGTH_SHORT).show();
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
        public String getDefaultMac() {
            return DEFAULT_PRINTER_MAC;
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
            final String targetMac = (macAddress == null || macAddress.isEmpty()) ? DEFAULT_PRINTER_MAC : macAddress;
            new Thread(() -> {
                BluetoothSocket socket = null;
                try {
                    byte[] data = Base64.decode(textBase64, Base64.DEFAULT);
                    BluetoothAdapter adapter = BluetoothAdapter.getDefaultAdapter();
                    if (adapter == null) throw new Exception("ဖုန်းတွင် Bluetooth မရှိပါ");
                    if (!adapter.isEnabled()) throw new Exception("ဖုန်း Bluetooth ဖွင့်ထားပေးပါ");

                    BluetoothDevice device = adapter.getRemoteDevice(targetMac);
                    @SuppressLint("MissingPermission") BluetoothSocket tmpSocket = device.createRfcommSocketToServiceRecord(SPP_UUID);
                    socket = tmpSocket;
                    adapter.cancelDiscovery();
                    socket.connect();

                    OutputStream os = socket.getOutputStream();
                    os.write(data);
                    os.flush();
                    Thread.sleep(600);
                    socket.close();
                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "ZyWell (Printer001) ပရင့် ထုတ်ပြီးပါပြီ", Toast.LENGTH_SHORT).show());
                } catch (Exception e) {
                    final String err = e.getMessage();
                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "Printer ချိတ်မရပါ: " + err, Toast.LENGTH_LONG).show());
                } finally {
                    try { if (socket != null) socket.close(); } catch(Exception ignored){}
                }
            }).start();
        }
    }

    private void showConfigDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("POS Server ချိတ်ဆက်ရန် IP");
        final EditText input = new EditText(this);
        input.setHint("ဥပမာ - http://localhost:8080");
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
