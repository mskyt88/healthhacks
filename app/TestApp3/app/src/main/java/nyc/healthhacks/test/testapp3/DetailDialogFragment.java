package nyc.healthhacks.test.testapp3;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v4.app.DialogFragment;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.TextView;

/**
 * Created by mskyt on 4/9/2017.
 */

public class DetailDialogFragment extends DialogFragment {

    protected RestaurantInfo info;
    protected TextView nameTextView;
    protected TextView categoryTextView;
    protected TextView ratingTextView;

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        // Get the layout inflater
        LayoutInflater inflater = getActivity().getLayoutInflater();

        // Inflate and set the layout for the dialog
        // Pass null as the parent view because its going in the dialog layout
        View view = inflater.inflate(R.layout.detail_dialog, null);
        builder.setView(view);

        info = new RestaurantInfo( this.getArguments() );

        builder.setPositiveButton("routrize", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                // User cancelled the dialog
                }
        } ).setNegativeButton("close", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // User cancelled the dialog
                    }
                });

        nameTextView = (TextView) view.findViewById(R.id.detail_name);
        nameTextView.setText( info.name );

        categoryTextView = (TextView) view.findViewById(R.id.detail_category);
        categoryTextView.setText( info.category );

        ratingTextView = (TextView) view.findViewById(R.id.detail_rating);
        ratingTextView.setText( String.format("%.1f", info.rating) );

        // Create the AlertDialog object and return it
        return builder.create();
    }

}
