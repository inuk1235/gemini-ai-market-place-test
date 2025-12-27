package com.example.marketplacealert

import kotlinx.coroutines.delay

object BackendApi {
    suspend fun search(keyword: String, location: String, radiusKm: Int): SearchResponse {
        // Replace with real networking (Retrofit/OkHttp).
        delay(500)
        return SearchResponse(
            listOf(
                Listing(
                    id = "demo",
                    title = "Sample Listing: $keyword",
                    price = "$${radiusKm * 10}",
                    link = "https://facebook.com/marketplace"
                )
            )
        )
    }
}
