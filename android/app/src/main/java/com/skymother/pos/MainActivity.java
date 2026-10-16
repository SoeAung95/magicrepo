package com.skymother.pos;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.Base64;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.OutputStream;
import java.lang.reflect.Method;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends Activity {
    private WebView webView;
    private SharedPreferences prefs;
    private ValueCallback<Uri[]> filePathCallback;
    private static final int FILE_CHOOSER_REQUEST_CODE = 1001;
    private static final UUID SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    private static final String DEFAULT_PRINTER_MAC = "AB:0D:9E:AD:7F:9B";

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        setContentView(webView);

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

        // Logo ပုံ ရွေးချယ်ခွင့် (WebChromeClient File Chooser)
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
                if (MainActivity.this.filePathCallback != null) {
                    MainActivity.this.filePathCallback.onReceiveValue(null);
                }
                MainActivity.this.filePathCallback = filePathCallback;

                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("image/*");
                try {
                    startActivityForResult(Intent.createChooser(intent, "Logo ပုံ ရွေးချယ်ပါ"), FILE_CHOOSER_REQUEST_CODE);
                } catch (Exception e) {
                    MainActivity.this.filePathCallback = null;
                    return false;
                }
                return true;
            }
        });

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
                        Toast.makeText(MainActivity.this, "RawBT App သို့ ပို့၍မရပါ", Toast.LENGTH_SHORT).show();
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

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == FILE_CHOOSER_REQUEST_CODE) {
            if (filePathCallback != null) {
                Uri[] results = null;
                if (resultCode == Activity.RESULT_OK && data != null) {
                    String dataString = data.getDataString();
                    if (dataString != null) {
                        results = new Uri[]{Uri.parse(dataString)};
                    }
                }
                filePathCallback.onReceiveValue(results);
                filePathCallback = null;
            }
        }
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

        @SuppressLint("MissingPermission")
        @JavascriptInterface
        public String getBluetoothDevices() {
            JSONArray arr = new JSONArray();
            try {
                BluetoothAdapter adapter = BluetoothAdapter.getDefaultAdapter();
                if (adapter != null && adapter.isEnabled()) {
                    Set<BluetoothDevice> paired = adapter.getBondedDevices();
                    for (BluetoothDevice d : paired) {
                        JSONObject obj = new JSONObject();
                        String name = d.getName();
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

        @SuppressLint("MissingPermission")
        @JavascriptInterface
        public void printBluetooth(String macAddress, String textBase64) {
            final String targetMac = (macAddress == null || macAddress.isEmpty()) ? DEFAULT_PRINTER_MAC : macAddress;
            new Thread(() -> {
                BluetoothSocket socket = null;
                String detailedError = "";
                boolean connected = false;

                try {
                    byte[] data = Base64.decode(textBase64, Base64.DEFAULT);
                    BluetoothAdapter adapter = BluetoothAdapter.getDefaultAdapter();
                    if (adapter == null) throw new Exception("Bluetooth Hardware မရှိပါ");
                    if (!adapter.isEnabled()) throw new Exception("Bluetooth ပိတ်ထားပါသည်");

                    BluetoothDevice device = adapter.getRemoteDevice(targetMac);
                    try { adapter.cancelDiscovery(); } catch (Exception ignored) {}

                    try {
                        socket = device.createInsecureRfcommSocketToServiceRecord(SPP_UUID);
                        socket.connect();
                        connected = true;
                    } catch (Exception e1) {
                        detailedError += "[Insecure SPP: " + e1.getMessage() + "] ";
                    }

                    if (!connected) {
                        try {
                            socket = device.createRfcommSocketToServiceRecord(SPP_UUID);
                            socket.connect();
                            connected = true;
                        } catch (Exception e2) {
                            detailedError += "[Secure SPP: " + e2.getMessage() + "] ";
                        }
                    }

                    if (!connected) {
                        try {
                            Method m = device.getClass().getMethod("createRfcommSocket", new java.lang.Class[]{int.class});
                            socket = (BluetoothSocket) m.invoke(device, 1);
                            socket.connect();
                            connected = true;
                        } catch (Exception e3) {
                            detailedError += "[Reflection Port 1: " + e3.getMessage() + "]";
                        }
                    }

                    if (!connected || socket == null) {
                        throw new Exception("Socket ချိတ်မရပါ -> " + detailedError);
                    }

                    OutputStream os = socket.getOutputStream();
                    os.write(data);
                    os.flush();
                    Thread.sleep(600);
                    socket.close();

                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "ZyWell ပရင့် အောင်မြင်ပါသည်", Toast.LENGTH_SHORT).show());

                } catch (Exception e) {
                    final String errMsg = e.getMessage();
                    runOnUiThread(() -> {
                        new AlertDialog.Builder(MainActivity.this)
                                .setTitle("Printer Error")
                                .setMessage("Error: " + errMsg + ". RawBT အရန်စနစ်ဖြင့် ထုတ်ယူမည်လား?")
                                .setPositiveButton("RawBT ဖြင့် ထုတ်မည်", (dialog, which) -> {
                                    try {
                                        Intent intent = new Intent(Intent.ACTION_VIEW);
                                        intent.setData(Uri.parse("rawbt:base64," + textBase64));
                                        startActivity(intent);
                                    } catch (Exception ex) {
                                        Toast.makeText(MainActivity.this, "RawBT App မရှိပါ", Toast.LENGTH_SHORT).show();
                                    }
                                })
                                .setNegativeButton("ပိတ်မည်", null)
                                .show();
                    });
                } finally {
                    try { if (socket != null) socket.close(); } catch (Exception ignored) {}
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
