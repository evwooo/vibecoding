"use client";

import { Map as GoogleMap, AdvancedMarker, InfoWindow, useMap } from "@vis.gl/react-google-maps";
import { useEffect, useState, useCallback } from "react";
import type { Location } from "@/app/page";

interface MapProps {
  locations: Location[];
  selectedLocation: Location | null;
  onDeselectLocation?: () => void;
}

// Category to color mapping
const CATEGORY_COLORS: { [key: string]: string } = {
  'Restaurant': '#FF6B6B',
  'Tourist Attraction': '#4ECDC4',
  'Hotel': '#45B7D1',
  'Beach': '#F7DC6F',
  'Museum': '#BB8FCE',
  'Park': '#82E0AA',
  'Shopping': '#F8C471',
  'Entertainment': '#FF8A80',
  'Transportation': '#90CAF9',
  'Other': '#A0A0A0'
};

// Category to emoji mapping
const CATEGORY_EMOJIS: { [key: string]: string } = {
  'Restaurant': '🍽️',
  'Tourist Attraction': '🗼',
  'Hotel': '🏨',
  'Beach': '🏖️',
  'Museum': '🏛️',
  'Park': '🌳',
  'Shopping': '🛍️',
  'Entertainment': '🎭',
  'Transportation': '🚌',
  'Other': '📍'
};

export default function Map({ locations, selectedLocation, onDeselectLocation }: MapProps) {
  const [center, setCenter] = useState({ lat: 20, lng: 0 });
  const [zoom, setZoom] = useState(2);
  const [activeMarker, setActiveMarker] = useState<string | null>(null);
  const mapInstance = useMap();

  useEffect(() => {
    if (selectedLocation) {
      setCenter({ lat: selectedLocation.lat, lng: selectedLocation.lng });
      setZoom(12);
      setActiveMarker(selectedLocation.id);
    }
  }, [selectedLocation]);

  const handleMarkerClick = useCallback((location: Location) => {
    setActiveMarker(activeMarker === location.id ? null : location.id);
    setCenter({ lat: location.lat, lng: location.lng });
    setZoom(Math.max(zoom, 10));
  }, [activeMarker, zoom]);

  // Handle map interactions that should deselect the current location
  const handleMapInteraction = useCallback(() => {
    if (selectedLocation && onDeselectLocation) {
      onDeselectLocation();
    }
  }, [selectedLocation, onDeselectLocation]);

  const renderStars = (rating: number) => {
    return (
      <div className="flex items-center space-x-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <span
            key={star}
            className={`text-sm ${
              star <= rating ? 'text-yellow-400' : 'text-gray-300'
            }`}
          >
            ★
          </span>
        ))}
      </div>
    );
  };

  const CustomMarker = ({ location }: { location: Location }) => {
    const color = CATEGORY_COLORS[location.category] || CATEGORY_COLORS['Other'];
    const emoji = CATEGORY_EMOJIS[location.category] || CATEGORY_EMOJIS['Other'];
    
    return (
      <div
        className="relative cursor-pointer transform transition-transform hover:scale-110"
        onClick={() => handleMarkerClick(location)}
      >
        <div
          className="w-8 h-8 rounded-full border-2 border-white shadow-lg flex items-center justify-center text-white font-bold"
          style={{ backgroundColor: color }}
        >
          <span className="text-sm">{emoji}</span>
        </div>
        {selectedLocation?.id === location.id && (
          <div className="absolute -top-1 -left-1 w-10 h-10 rounded-full border-2 border-blue-500 animate-pulse"></div>
        )}
      </div>
    );
  };

  const fitBounds = useCallback(() => {
    if (!mapInstance || locations.length === 0) return;
    
    const bounds = new google.maps.LatLngBounds();
    locations.forEach(location => {
      bounds.extend(new google.maps.LatLng(location.lat, location.lng));
    });
    
    mapInstance.fitBounds(bounds);
    
    // Adjust zoom if there's only one location
    if (locations.length === 1) {
      mapInstance.setZoom(12);
    }
  }, [mapInstance, locations]);

  return (
    <div className="flex-grow h-full w-full">
      <GoogleMap
        mapId={"travel_map"}
        center={center}
        zoom={zoom}
        gestureHandling={"greedy"}
        disableDefaultUI={false}
        style={{ width: "100%", height: "100%" }}
        zoomControl={true}
        mapTypeControl={true}
        scaleControl={true}
        streetViewControl={true}
        rotateControl={true}
        fullscreenControl={true}
        onDragend={handleMapInteraction}
        onZoomChanged={handleMapInteraction}
      >
        {locations.map((location) => (
          <AdvancedMarker
            key={location.id}
            position={location}
            title={location.name}
          >
            <CustomMarker location={location} />
          </AdvancedMarker>
        ))}

        {/* Info Windows */}
        {locations.map((location) => (
          activeMarker === location.id && (
            <InfoWindow
              key={`info-${location.id}`}
              position={location}
              onCloseClick={() => setActiveMarker(null)}
            >
              <div className="p-3 max-w-xs">
                <h3 className="font-semibold text-lg mb-2">{location.name}</h3>
                
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                      {location.category}
                    </span>
                    <span className="text-sm text-gray-600">{location.dateVisited}</span>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-600">Rating:</span>
                    {renderStars(location.rating)}
                  </div>
                  
                  {location.notes && (
                    <div>
                      <p className="text-sm text-gray-600 font-medium mb-1">Notes:</p>
                      <p className="text-sm text-gray-700">{location.notes}</p>
                    </div>
                  )}
                </div>
              </div>
            </InfoWindow>
          )
        ))}
      </GoogleMap>

      {/* Map Controls */}
      <div className="absolute top-4 left-4 space-y-2">
        <button
          onClick={fitBounds}
          className="bg-white shadow-lg rounded-lg p-3 hover:bg-gray-50 transition-colors"
          title="Fit all locations"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5h-4m4 0v-4m0 4l-5-5" />
          </svg>
        </button>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg p-3">
        <h4 className="font-semibold text-sm mb-2">Categories</h4>
        <div className="grid grid-cols-2 gap-1 text-xs">
          {Object.entries(CATEGORY_COLORS).map(([category, color]) => (
            <div key={category} className="flex items-center space-x-1">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: color }}
              ></div>
              <span>{category}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Location counter */}
      <div className="absolute top-4 right-4 bg-white rounded-lg shadow-lg p-3">
        <div className="text-sm font-medium text-gray-700">
          {locations.length} locations
        </div>
      </div>
    </div>
  );
}
