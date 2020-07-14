package org.tensorflow.lite.examples.posenet;

import android.content.Intent;
import android.graphics.Camera;
import android.graphics.Typeface;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import android.net.Uri;
import android.os.Bundle;
import android.provider.Telephony;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Button;

public class activity2 extends AppCompatActivity implements View.OnClickListener{
    private CardView websiteCard, exerciseCard;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);
        // defining the Cards
        websiteCard = (CardView) findViewById(R.id.website_card);
        exerciseCard = (CardView) findViewById(R.id.exercise_card);
        // Add Click listener to the cards
        websiteCard.setOnClickListener(this);
        exerciseCard.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        Intent i;

        switch (v.getId()) {
            case R.id.exercise_card : i = new Intent(this, MainActivity.class); break ;
            default: break ;
        }

    }
}