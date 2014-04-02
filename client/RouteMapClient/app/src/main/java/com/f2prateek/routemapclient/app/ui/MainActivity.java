package com.f2prateek.routemapclient.app.ui;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import com.f2prateek.routemapclient.app.R;

public class MainActivity extends Activity {

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    //setContentView(R.layout.activity_main);

    if (savedInstanceState == null) {
      VenuesMapFragment fragment = new VenuesMapFragment();
      getFragmentManager().beginTransaction().add(android.R.id.content, fragment).commit();
    }
  }

  @Override
  public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.main, menu);
    return true;
  }

  @Override
  public boolean onOptionsItemSelected(MenuItem item) {
    int id = item.getItemId();
    return super.onOptionsItemSelected(item);
  }
}
