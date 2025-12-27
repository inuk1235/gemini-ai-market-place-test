package com.example.marketplacealert

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters

class SearchWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {
    override suspend fun doWork(): Result {
        val keyword = inputData.getString("keyword") ?: return Result.failure()
        val location = inputData.getString("location") ?: return Result.failure()
        val radiusKm = inputData.getInt("radiusKm", 10)

        val response = BackendApi.search(keyword, location, radiusKm)
        val newListings = response.newListings

        if (newListings.isNotEmpty()) {
            showNotification(newListings.first())
        }

        return Result.success()
    }

    private fun showNotification(listing: Listing) {
        val channelId = "marketplace_alerts"
        val manager =
            applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "Marketplace Alerts",
                NotificationManager.IMPORTANCE_HIGH
            )
            manager.createNotificationChannel(channel)
        }

        val notification = NotificationCompat.Builder(applicationContext, channelId)
            .setSmallIcon(R.drawable.ic_alert)
            .setContentTitle(listing.title)
            .setContentText("${listing.price} - Tap to view")
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()

        manager.notify(listing.id.hashCode(), notification)
    }
}
