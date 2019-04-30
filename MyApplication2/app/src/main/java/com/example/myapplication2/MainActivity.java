package com.example.myapplication2;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "TestActivity";
    private HttpConnection httpConn = HttpConnection.getInstance();

    Button.OnClickListener t = new Button.OnClickListener(){
        @Override
        public void  onClick(View v){
            EditText edtxt = (EditText)findViewById(R.id.editText);
            EditText edtxt2 = (EditText)findViewById(R.id.editText2);
            EditText edtxt3 = (EditText)findViewById(R.id.editText3);
            sendData(edtxt.getText().toString(), edtxt2.getText().toString(), edtxt3.getText().toString());
        }
    };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        findViewById(R.id.button).setOnClickListener(t);
    }

    private void sendData(final String a, final String b, final String c){
        new Thread(){
            public void run(){
                httpConn.requestWebServer(a,b, callback, c);
            }
        }.start();
    }

    private final Callback callback = new Callback() {
        @Override
        public void onFailure(Call call, IOException e) {
            Log.d(TAG, "콜백오류:"+e.getMessage());
        }

        @Override
        public void onResponse(Call call, Response response) throws IOException {
            String body = response.body().string();
            Log.d(TAG, "서버에서 응답한 Body:" + body);
            TextView txt = (TextView)findViewById(R.id.textView);
            txt.setText(body);
        }
    };
}
