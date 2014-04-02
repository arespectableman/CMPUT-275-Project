package com.f2prateek.routemapclient.app.ui;

import android.location.Location;
import android.widget.Toast;
import com.f2prateek.routemapclient.app.FoursquareFactory;
import com.f2prateek.routemapclient.app.model.foursquare.FoursquareVenue;
import com.f2prateek.routemapclient.app.model.foursquare.VenuesResponse;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.maps.android.clustering.ClusterManager;
import pl.charmas.android.reactivelocation.ReactiveLocationProvider;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;
import rx.util.functions.Action1;

public class VenuesMapFragment extends MapFragment implements Callback<VenuesResponse> {

  @Override public void onStart() {
    super.onStart();
    ReactiveLocationProvider locationProvider = new ReactiveLocationProvider(getActivity());
    locationProvider.getLastKnownLocation().subscribe(new Action1<Location>() {
      @Override
      public void call(Location location) {
        getMap().moveCamera(CameraUpdateFactory.newLatLngZoom(
            new LatLng(location.getLatitude(), location.getLongitude()), 10));
        FoursquareFactory.getInstance()
            .venues(location.getLatitude(), location.getLongitude(), VenuesMapFragment.this);
      }
    });
  }

  @Override public void success(VenuesResponse response, Response raw) {
    ClusterManager clusterManager = new ClusterManager<FoursquareVenue>(getActivity(), getMap());
    clusterManager.addItems(response.venues);

    getMap().setOnCameraChangeListener(clusterManager);
    getMap().setOnMarkerClickListener(clusterManager);
  }

  @Override public void failure(RetrofitError error) {
    Toast.makeText(getActivity(), "An unknown error occurred.", Toast.LENGTH_LONG).show();
  }
}
