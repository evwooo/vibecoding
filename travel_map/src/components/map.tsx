"use client";

import { Map as GoogleMap, Marker, AdvancedMarker } from "@vis.gl/react-google-maps";
import { useEffect, useState } from "react";
import type { Location } from "@/app/page";

interface MapProps {
  locations: Location[];
  selectedLocation: Location | null;
}

export default function Map({ locations, selectedLocation }: MapProps) {
  const [center, setCenter] = useState({ lat: 20, lng: 0 });
  const [zoom, setZoom] = useState(2);

  useEffect(() => {
    if (selectedLocation) {
      setCenter({ lat: selectedLocation.lat, lng: selectedLocation.lng });
      setZoom(10);
    }
  }, [selectedLocation]);

  return (
    <div className="flex-grow h-full">
      <GoogleMap
        mapId={"travel_map"}
        center={center}
        zoom={zoom}
        gestureHandling={"greedy"}
        disableDefaultUI={true}
      >
        {locations.map((location, index) => (
          <AdvancedMarker key={index} position={location} title={location.name} />
        ))}
      </GoogleMap>
    </div>
  );
}
