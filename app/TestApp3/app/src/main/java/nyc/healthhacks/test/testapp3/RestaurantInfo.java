package nyc.healthhacks.test.testapp3;

import android.os.Bundle;
import android.util.Log;

import com.google.android.gms.maps.model.LatLng;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by mskyt on 4/9/2017.
 */

public class RestaurantInfo extends Object {
    public String rid;
    public String name;
    public LatLng pos;
    public double rating;
    public String category;

    public RestaurantInfo( JSONObject json ) {
        try {
            this.rid = json.getString("id");
            this.pos = new LatLng(
                    json.getJSONObject("coordinates").getDouble("latitude"),
                    json.getJSONObject("coordinates").getDouble("longitude") );
            this.name = json.getString("name");
            this.rating = json.getDouble("rating");

            this.category = "";
            JSONArray categories = json.getJSONArray("categories");
            for( int i=0; i<categories.length(); i++) {
                this.category += categories.getJSONObject(i).getString("title");
                if( i < categories.length()-1 ) {
                    this.category += ", ";
                }
            }

        } catch( JSONException e ){
            Log.e( "JSON parsing failed : ", e.toString() );
        }
    }

    public RestaurantInfo( Bundle bundle ) {
        this.rid = bundle.getString("id");
        this.name = bundle.getString("name");
        this.rating = bundle.getDouble("rating");
        this.category = bundle.getString("category");
    }

    public Bundle toBundle() {
        Bundle bundle = new Bundle();
        bundle.putString( "id", this.rid );
        bundle.putString( "name", this.name );
        bundle.putDouble( "rating", this.rating );
        bundle.putString( "category", this.category );
        return bundle;
    }
}
