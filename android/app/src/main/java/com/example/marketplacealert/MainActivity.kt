package com.example.marketplacealert

import android.os.Bundle
import android.widget.AutoCompleteTextView
import android.widget.Button
import android.widget.EditText
import android.widget.SeekBar
import androidx.appcompat.app.AppCompatActivity
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.workDataOf
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {
    private lateinit var keywordInput: EditText
    private lateinit var locationInput: AutoCompleteTextView
    private lateinit var radiusSeek: SeekBar
    private lateinit var startStopButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        keywordInput = findViewById(R.id.keywordInput)
        locationInput = findViewById(R.id.locationInput)
        radiusSeek = findViewById(R.id.radiusSeek)
        startStopButton = findViewById(R.id.startStopButton)

        startStopButton.setOnClickListener {
            val keyword = keywordInput.text.toString().trim()
            val location = locationInput.text.toString().trim()
            val radiusKm = radiusSeek.progress

            scheduleBackgroundSearch(keyword, location, radiusKm)
        }
    }

    private fun scheduleBackgroundSearch(keyword: String, location: String, radiusKm: Int) {
        val data = workDataOf(
            "keyword" to keyword,
            "location" to location,
            "radiusKm" to radiusKm
        )

        val request = PeriodicWorkRequestBuilder<SearchWorker>(
            15,
            TimeUnit.MINUTES
        ).setInputData(data).build()

        WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "MarketplaceSearch",
            ExistingPeriodicWorkPolicy.REPLACE,
            request
        )
    }
}
