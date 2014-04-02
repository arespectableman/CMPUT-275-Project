package com.f2prateek.routemapclient.app.ui;

import android.content.Context;
import android.location.Location;
import android.widget.Toast;
import com.f2prateek.routemapclient.app.FoursquareFactory;
import com.f2prateek.routemapclient.app.R;
import com.f2prateek.routemapclient.app.model.foursquare.FoursquareVenue;
import com.f2prateek.routemapclient.app.model.foursquare.VenuesResponse;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.maps.android.clustering.ClusterManager;
import com.google.maps.android.clustering.view.DefaultClusterRenderer;
import java.util.Arrays;
import pl.charmas.android.reactivelocation.ReactiveLocationProvider;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;
import rx.util.functions.Action1;

public class VenuesMapFragment extends MapFragment implements Callback<VenuesResponse>,
    ClusterManager.OnClusterItemClickListener<FoursquareVenue> {

  ClusterManager<FoursquareVenue> clusterManager;
  Location lastKnownLocation;

  @Override public void onStart() {
    super.onStart();

    getMap().setMyLocationEnabled(true);
    getMap().setIndoorEnabled(true);
    getMap().getUiSettings().setAllGesturesEnabled(true);

    ReactiveLocationProvider locationProvider = new ReactiveLocationProvider(getActivity());
    locationProvider.getLastKnownLocation().subscribe(new Action1<Location>() {
      @Override
      public void call(Location location) {
        lastKnownLocation = location;
        centerMap(location);

        FoursquareFactory.getInstance()
            .venues(new FoursquareFactory.Location(location.getLatitude(), location.getLongitude()),
                VenuesMapFragment.this);
      }
    });
  }

  @Override public void success(VenuesResponse response, Response raw) {
    clusterManager = new ClusterManager<FoursquareVenue>(getActivity(), getMap());
    clusterManager.setRenderer(new VenueRenderer(getActivity(), getMap(), clusterManager));

    getMap().setOnCameraChangeListener(clusterManager);
    getMap().setOnMarkerClickListener(clusterManager);

    clusterManager.addItems(response.venues);
    clusterManager.cluster();
    clusterManager.setOnClusterItemClickListener(this);
  }

  private void centerMap(Location location) {
    LatLng moveTo = new LatLng(location.getLatitude(), location.getLongitude());
    getMap().animateCamera(CameraUpdateFactory.newLatLngZoom(moveTo, 10));
  }

  @Override public void failure(RetrofitError error) {
    Toast.makeText(getActivity(), "An unknown error occurred.", Toast.LENGTH_LONG).show();
  }

  @Override public boolean onClusterItemClick(FoursquareVenue foursquareVenue) {
    FoursquareFactory.getInstance()
        .route(Arrays.asList(new FoursquareFactory.Location(lastKnownLocation.getLatitude(),
                lastKnownLocation.getLongitude()),
            new FoursquareFactory.Location(foursquareVenue.location.lat,
                foursquareVenue.location.lat)
        ), new Callback<String>() {
          @Override public void success(String s, Response response) {
            Toast.makeText(getActivity(), "Got " + s, Toast.LENGTH_LONG).show();
          }

          @Override public void failure(RetrofitError error) {
            Toast.makeText(getActivity(), "An unknown error occurred.", Toast.LENGTH_LONG).show();
          }
        });
    return false;
  }

  static class VenueRenderer extends DefaultClusterRenderer<FoursquareVenue> {

    public VenueRenderer(Context context, GoogleMap map,
        ClusterManager<FoursquareVenue> clusterManager) {
      super(context, map, clusterManager);
    }

    @Override
    protected void onBeforeClusterItemRendered(FoursquareVenue venue, MarkerOptions markerOptions) {
      markerOptions.icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_location_marker))
          .title(venue.name);
    }
  }
}
