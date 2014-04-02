package com.f2prateek.routemapclient.app;

import com.f2prateek.routemapclient.app.model.foursquare.VenuesResponse;
import java.util.List;
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
        new RestAdapter.Builder().setEndpoint("http://b07ea95.ngrok.com").build();
    instance = restAdapter.create(Foursquare.class);
  }

  public static Foursquare getInstance() {
    if (instance == null) {
      throw new IllegalStateException("init must be called before accessing instance.");
    }
    return instance;
  }

  public interface Foursquare {
    @GET("/venues") void venues(@Query("location") Location location, Callback<VenuesResponse> cb);

    @GET("/route") void route(@Query("locations") List<Location> location, Callback<String> cb);
  }

  public static class Location {
    public double lat;
    public double lng;

    public Location(double lat, double lng) {
      this.lat = lat;
      this.lng = lng;
    }
  }
}
