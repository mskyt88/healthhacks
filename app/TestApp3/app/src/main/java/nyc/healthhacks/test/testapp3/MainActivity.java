package nyc.healthhacks.test.testapp3;

import android.app.Activity;
import android.app.DownloadManager;
import android.app.Fragment;
import android.app.FragmentTransaction;
import android.support.design.widget.BottomSheetBehavior;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.FragmentActivity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.VisibleRegion;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;


public class MainActivity extends FragmentActivity implements OnMapReadyCallback, View.OnClickListener, GoogleMap.OnMarkerClickListener {

    private List<RestaurantInfo> restInfos;

    private GoogleMap googleMap;
    private RequestQueue httpQueue;

    private Button searchButton;
    private TextView logTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        restInfos = new ArrayList<RestaurantInfo>();

        // google map
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        // http request queue
        httpQueue = Volley.newRequestQueue(this);

        // search button
        searchButton = (Button)findViewById(R.id.search_button);
        searchButton.setOnClickListener(this);

        // logger
        logTextView = (TextView)findViewById(R.id.log_text);

    }

    @Override
    public void onMapReady(GoogleMap _googleMap) {
        googleMap = _googleMap;

        LatLng columbia = new LatLng(40.809575, -73.960733);
        googleMap.moveCamera(CameraUpdateFactory.newLatLng(columbia));
        googleMap.moveCamera(CameraUpdateFactory.zoomTo(15));

        googleMap.setOnMarkerClickListener( this );

        // TODO: call this later
        this.searchInRegion( null );
    }

    @Override
    public void onClick(View v) {
        if( v == searchButton ){
            if( googleMap != null ) {
                this.searchInRegion( googleMap.getProjection().getVisibleRegion() );
            }
        }
    }

    protected void searchInRegion( VisibleRegion region ) {
        LatLng ne, sw;
        if( region != null ) {
            ne = region.latLngBounds.northeast;
            sw = region.latLngBounds.southwest;
        } else {
            ne = new LatLng( 40.816857, -73.952837 );
            sw = new LatLng( 40.802292, -73.968629 );
        }

        // clear markers on the map
        restInfos.clear();
        onListUpdated();

        // query to server
        String url_param = String.format( "x1=%f&y1=%f&x2=%f&y2=%f", sw.latitude, sw.longitude, ne.latitude, ne.longitude );
        logTextView.setText( url_param );

        String url = "http://healthhack.mybluemix.net/pass?"+url_param;

        // Request a string response from the provided URL.
        StringRequest request = new StringRequest(com.android.volley.Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        try {
                            JSONObject json_response = new JSONObject(response);
                            JSONArray infos = json_response.getJSONArray("results");

                            restInfos.clear();
                            for( int i=0; i < infos.length(); i++ ) {
                                JSONObject info = infos.getJSONObject(i);
                                restInfos.add( new RestaurantInfo(info) );
                            }
                            onListUpdated();

                        } catch( JSONException e ) {
                            logTextView.setText( "JSON parsing failed" );
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                logTextView.setText("Query failed.");
            }
        });

        // Add the request to the RequestQueue.
        httpQueue.add(request);
    }

    protected void onListUpdated() {
        if( googleMap != null ) {
            googleMap.clear();

            for( RestaurantInfo info : restInfos ) {
                MarkerOptions marker = new MarkerOptions();

                marker.position(info.pos).title(info.name);

                if (info.rating < 3.9) {
                    marker.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED));
                } else if (info.rating < 4.2) {
                    marker.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_ORANGE));
                } else{
                    marker.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN));
                }

                googleMap.addMarker(marker);
            }
        }
    }


    @Override
    public boolean onMarkerClick(Marker marker) {
        //logTextView.setText( "touched : " + marker.getTitle() );
        for( RestaurantInfo info : restInfos ) {
            if( marker.getTitle().equals( info.name ) ) {
                logTextView.setText( info.name + " touched" );

                DialogFragment dialog = new DetailDialogFragment();
                dialog.setArguments( info.toBundle() );
                dialog.show(getSupportFragmentManager(), "DetailDialogFragment");
            }
        }
        return false;
    }
}
