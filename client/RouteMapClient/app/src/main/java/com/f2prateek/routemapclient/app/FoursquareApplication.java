package com.f2prateek.routemapclient.app;

import android.app.Application;

public class FoursquareApplication extends Application {

  @Override public void onCreate() {
    super.onCreate();

    init();
  }

  public void init() {
    PreferenceFactory.init(this);
    FoursquareFactory.init();
  }
}
