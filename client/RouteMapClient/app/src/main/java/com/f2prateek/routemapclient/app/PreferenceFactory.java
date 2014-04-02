package com.f2prateek.routemapclient.app;

import android.app.Application;
import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;

public class PreferenceFactory {

  private static PreferenceFactory instance;

  private PreferenceFactory(SharedPreferences sharedPreferences) {
  }

  public static void init(Application application) {
    instance = new PreferenceFactory(PreferenceManager.getDefaultSharedPreferences(application));
  }

  public static PreferenceFactory getInstance(Context context) {
    if (instance == null) {
      throw new IllegalStateException("init must be called before accessing instance.");
    }
    return instance;
  }
}
