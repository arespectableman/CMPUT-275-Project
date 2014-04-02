package com.f2prateek.routemapclient.app;

import com.f2prateek.routemapclient.app.model.foursquare.VenuesResponse;
import retrofit.Callback;
import retrofit.RestAdapter;
import retrofit.http.GET;
import retrofit.http.Query;

public class FoursquareFactory {

  private static Foursquare instance;

  private FoursquareFactory() {
    // no instances
  }

  public static void init() {
    RestAdapter restAdapter =
        new RestAdapter.Builder().setEndpoint("http://113d2b7c.ngrok.com").build();
    instance = restAdapter.create(Foursquare.class);
  }

  public static Foursquare getInstance() {
    if (instance == null) {
      throw new IllegalStateException("init must be called before accessing instance.");
    }
    return instance;
  }

  public interface Foursquare {
    @GET("/venues") void venues(@Query("lat") double latitude, @Query("lng") double longitude,
        Callback<VenuesResponse> cb);
  }
}
