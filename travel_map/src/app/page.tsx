"use client";

import { useState, useEffect } from "react";
import { APIProvider } from "@vis.gl/react-google-maps";
import Map from "@/components/map";
import Sidebar from "@/components/sidebar";

export interface Location {
  name: string;
  lat: number;
  lng: number;
}

const LOCATION_STORAGE_KEY = "visited_locations";

export default function Home() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null);

  // Load locations from localStorage on initial render
  useEffect(() => {
    const savedLocations = localStorage.getItem(LOCATION_STORAGE_KEY);
    if (savedLocations) {
      setLocations(JSON.parse(savedLocations));
    }
  }, []);

  // Save locations to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(LOCATION_STORAGE_KEY, JSON.stringify(locations));
  }, [locations]);

  const addLocation = (location: Location) => {
    const newLocations = [...locations, location];
    setLocations(newLocations);
    setSelectedLocation(location);
  };

  const deleteLocation = (index: number) => {
    const newLocations = locations.filter((_, i) => i !== index);
    setLocations(newLocations);
  };

  return (
    <APIProvider apiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!}>
      <div className="flex h-screen font-sans">
        <Sidebar
          locations={locations}
          onAddLocation={addLocation}
          onDeleteLocation={deleteLocation}
          onSelectLocation={setSelectedLocation}
        />
        <Map locations={locations} selectedLocation={selectedLocation} />
      </div>
    </APIProvider>
  );
}