package com.example.myapplication2;

import android.util.Log;

import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;

public class HttpConnection {

    private OkHttpClient client;
    private static HttpConnection instance = new HttpConnection();
    public static HttpConnection getInstance(){
        return instance;
    }

    private HttpConnection(){this.client = new OkHttpClient();}

    public void requestWebServer(String parameter1, String parameter2, Callback callback, String se_ip){

        RequestBody body = new FormBody.Builder()
                .add("parameter1", parameter1)
                .add("parameter2", parameter2)
                .build();
        Request request = new Request.Builder()
                .url("http://192.168.43.190/teest.php")
                .post(body)
                .build();
        client.newCall(request).enqueue(callback);
    }
}


