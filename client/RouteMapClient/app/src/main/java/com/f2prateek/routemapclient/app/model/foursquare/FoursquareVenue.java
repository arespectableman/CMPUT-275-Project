package com.f2prateek.routemapclient.app.model.foursquare;

import com.google.android.gms.maps.model.LatLng;
import com.google.maps.android.clustering.ClusterItem;
import java.util.List;

/**
 * A model class representing a Foursquare venue.
 *
 * Only defines fields for a compact object.
 * https://developer.foursquare.com/docs/responses/venue
 *
 * Implements {@link com.google.maps.android.clustering.ClusterItem} directly to help memory.
 */
public class FoursquareVenue implements ClusterItem {
  public String id;
  public String name;
  public Boolean verified;
  public Contact contact;
  public Location location;
  public List<Category> categories;
  //public CompleteSpecial[] specials;
  //public HereNow hereNow;
  public Stats stats;
  public String url;

  //public Tips tips;
  //public TodoGroup todos;

  @Override public LatLng getPosition() {
    return new LatLng(location.lat, location.lng);
  }
}
