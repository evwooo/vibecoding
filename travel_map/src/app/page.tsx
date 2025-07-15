"use client";

import { useState, useEffect } from "react";
import { APIProvider } from "@vis.gl/react-google-maps";
import Map from "@/components/map";
import Sidebar from "@/components/sidebar";

export interface Location {
  id: string;
  name: string;
  lat: number;
  lng: number;
  category: string;
  notes: string;
  dateVisited: string;
  rating: number;
}

const LOCATION_STORAGE_KEY = "visited_locations";

export default function Home() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load locations from localStorage on initial render
  useEffect(() => {
    try {
      const savedLocations = localStorage.getItem(LOCATION_STORAGE_KEY);
      if (savedLocations) {
        const parsedLocations = JSON.parse(savedLocations);
        // Migrate old locations to new format
        const migratedLocations = parsedLocations.map((location: Partial<Location>, index: number) => ({
          id: location.id || `location-${index}`,
          name: location.name,
          lat: location.lat,
          lng: location.lng,
          category: location.category || "Other",
          notes: location.notes || "",
          dateVisited: location.dateVisited || new Date().toISOString().split('T')[0],
          rating: location.rating || 3
        }));
        setLocations(migratedLocations);
      }
    } catch (err) {
      setError("Failed to load saved locations");
      console.error("Error loading locations:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Save locations to localStorage whenever they change
  useEffect(() => {
    if (!isLoading) {
      try {
        localStorage.setItem(LOCATION_STORAGE_KEY, JSON.stringify(locations));
      } catch (err) {
        setError("Failed to save locations");
        console.error("Error saving locations:", err);
      }
    }
  }, [locations, isLoading]);

  const addLocation = (locationData: Omit<Location, 'id'>) => {
    const newLocation: Location = {
      ...locationData,
      id: `location-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    };
    const newLocations = [...locations, newLocation];
    setLocations(newLocations);
    setSelectedLocation(newLocation);
  };

  const updateLocation = (id: string, updates: Partial<Location>) => {
    setLocations(locations.map(loc => 
      loc.id === id ? { ...loc, ...updates } : loc
    ));
  };

  const deleteLocation = (id: string) => {
    const newLocations = locations.filter(loc => loc.id !== id);
    setLocations(newLocations);
    if (selectedLocation?.id === id) {
      setSelectedLocation(null);
    }
  };

  const onDeselectLocation = () => {
    setSelectedLocation(null);
  };

  const exportLocations = () => {
    const dataStr = JSON.stringify(locations, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    const exportFileDefaultName = `travel-map-locations-${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const importLocations = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const importedLocations = JSON.parse(e.target?.result as string);
        if (Array.isArray(importedLocations)) {
          setLocations(importedLocations);
          setError(null);
        } else {
          setError("Invalid file format");
        }
      } catch (err) {
        setError("Failed to import locations");
        console.error("Error importing locations:", err);
      }
    };
    reader.readAsText(file);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your travel map...</p>
        </div>
      </div>
    );
  }

  return (
    <APIProvider apiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!}>
      <div className="flex h-screen font-sans bg-gray-50">
        {error && (
          <div className="absolute top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-50">
            {error}
            <button 
              onClick={() => setError(null)}
              className="ml-2 hover:bg-red-600 px-2 py-1 rounded"
            >
              ×
            </button>
          </div>
        )}
        <Sidebar
          locations={locations}
          onAddLocation={addLocation}
          onUpdateLocation={updateLocation}
          onDeleteLocation={deleteLocation}
          onSelectLocation={setSelectedLocation}
          onExportLocations={exportLocations}
          onImportLocations={importLocations}
        />
        <Map locations={locations} selectedLocation={selectedLocation} onDeselectLocation={onDeselectLocation} />
      </div>
    </APIProvider>
  );
}