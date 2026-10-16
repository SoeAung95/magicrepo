package com.skymother.pos;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;

public class MainActivity extends Activity {
    private WebView webView;
    private SharedPreferences prefs;

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
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                showConfigDialog();
            }
        });

        webView.setOnLongClickListener(v -> {
            showConfigDialog();
            return true;
        });

        webView.loadUrl(serverUrl);
    }

    private void showConfigDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("POS Server ချိတ်ဆက်ရန် IP");
        final EditText input = new EditText(this);
        input.setHint("ဥပမာ - http://192.168.1.5:8080");
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
