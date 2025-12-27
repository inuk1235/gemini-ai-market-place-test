package com.example.marketplacealert

data class Listing(
    val id: String,
    val title: String,
    val price: String,
    val link: String
)

data class SearchResponse(
    val newListings: List<Listing>
)
