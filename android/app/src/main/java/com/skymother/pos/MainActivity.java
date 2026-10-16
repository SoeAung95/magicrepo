package com.skymother.pos;
import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.PendingIntent;
import android.bluetooth.*;
import android.content.*;
import android.content.pm.PackageManager;
import android.hardware.usb.*;
import android.net.Uri;
import android.os.*;
import android.util.Base64;
import android.webkit.*;
import android.widget.*;
import java.io.OutputStream;
import java.lang.reflect.Method;
import java.util.*;

public class MainActivity extends Activity {
    private WebView webView;
    private SharedPreferences prefs;
    private ValueCallback<Uri[]> filePathCallback;
    private static final UUID SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        setContentView(webView);
        prefs = getSharedPreferences("SkyMotherPOS", MODE_PRIVATE);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            List<String> perms = new ArrayList<>();
            perms.add(Manifest.permission.ACCESS_FINE_LOCATION);
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                perms.add(Manifest.permission.BLUETOOTH_CONNECT);
                perms.add(Manifest.permission.BLUETOOTH_SCAN);
            }
            requestPermissions(perms.toArray(new String[0]), 101);
        }

        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView w, ValueCallback<Uri[]> cb, FileChooserParams p) {
                filePathCallback = cb;
                Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                i.addCategory(Intent.CATEGORY_OPENABLE);
                i.setType("image/*");
                startActivityForResult(Intent.createChooser(i, "Logo ရွေးပါ"), 1001);
                return true;
            }
        });

        webView.addJavascriptInterface(new POSBridge(), "NativePrinter");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, String url) {
                if (!url.startsWith("http")) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); } catch(Exception e){}
                    return true;
                }
                return false;
            }
        });
        webView.setOnLongClickListener(v -> { showIpDialog(); return true; });
        webView.loadUrl(prefs.getString("server_url", "http://localhost:8080"));
    }

    @Override
    protected void onActivityResult(int req, int res, Intent d) {
        if (req == 1001 && filePathCallback != null) {
            Uri[] r = (res == RESULT_OK && d != null && d.getDataString() != null) ? new Uri[]{Uri.parse(d.getDataString())} : null;
            filePathCallback.onReceiveValue(r);
            filePathCallback = null;
        }
    }

    public class POSBridge {
        @JavascriptInterface public boolean isNative() { return true; }

        @SuppressLint("MissingPermission")
        @JavascriptInterface
        public void printBluetooth(String mac, String b64) {
            new Thread(() -> {
                BluetoothSocket sock = null;
                try {
                    byte[] data = Base64.decode(b64, Base64.DEFAULT);
                    BluetoothAdapter ad = BluetoothAdapter.getDefaultAdapter();
                    String target = (mac == null || mac.isEmpty()) ? "AB:0D:9E:AD:7F:9B" : mac;
                    BluetoothDevice dev = ad.getRemoteDevice(target);
                    try { ad.cancelDiscovery(); } catch(Exception ignored){}
                    try {
                        sock = dev.createInsecureRfcommSocketToServiceRecord(SPP_UUID);
                        sock.connect();
                    } catch(Exception e1) {
                        Method m = dev.getClass().getMethod("createRfcommSocket", new Class[]{int.class});
                        sock = (BluetoothSocket) m.invoke(dev, 1);
                        sock.connect();
                    }
                    OutputStream os = sock.getOutputStream();
                    os.write(data);
                    os.flush();
                    Thread.sleep(500);
                    sock.close();
                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "Bluetooth ပရင့်အောင်မြင်ပါသည်", Toast.LENGTH_SHORT).show());
                } catch(Exception e) {
                    printUsb(b64);
                }
            }).start();
        }

        @JavascriptInterface
        public void printUsb(String b64) {
            new Thread(() -> {
                try {
                    byte[] data = Base64.decode(b64, Base64.DEFAULT);
                    UsbManager m = (UsbManager) getSystemService(Context.USB_SERVICE);
                    for (UsbDevice dev : m.getDeviceList().values()) {
                        UsbInterface intf = dev.getInterface(0);
                        for (int j = 0; j < intf.getEndpointCount(); j++) {
                            UsbEndpoint ep = intf.getEndpoint(j);
                            if (ep.getDirection() == UsbConstants.USB_DIR_OUT) {
                                if (!m.hasPermission(dev)) {
                                    PendingIntent pi = PendingIntent.getBroadcast(MainActivity.this, 0, new Intent("USB_PERM"), PendingIntent.FLAG_IMMUTABLE);
                                    m.requestPermission(dev, pi);
                                    return;
                                }
                                UsbDeviceConnection c = m.openDevice(dev);
                                c.claimInterface(intf, true);
                                c.bulkTransfer(ep, data, data.length, 4000);
                                c.close();
                                runOnUiThread(() -> Toast.makeText(MainActivity.this, "USB ပရင့်အောင်မြင်ပါသည်", Toast.LENGTH_SHORT).show());
                                return;
                            }
                        }
                    }
                    runOnUiThread(() -> {
                        try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("rawbt:base64," + b64))); }
                        catch(Exception ex) { Toast.makeText(MainActivity.this, "Printer မတွေ့ပါ", Toast.LENGTH_SHORT).show(); }
                    });
                } catch(Exception e) {}
            }).start();
        }
    }

    private void showIpDialog() {
        EditText in = new EditText(this);
        in.setText(prefs.getString("server_url", "http://localhost:8080"));
        new AlertDialog.Builder(this).setTitle("Server IP").setView(in)
            .setPositiveButton("ချိတ်မည်", (d, w) -> {
                String u = in.getText().toString().trim();
                prefs.edit().putString("server_url", u).apply();
                webView.loadUrl(u);
            }).show();
    }
}