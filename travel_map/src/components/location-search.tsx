"use client";

import { useRef, useEffect } from "react";
import { useMapsLibrary } from "@vis.gl/react-google-maps";
import type { Location } from "@/app/page";

interface LocationSearchProps {
  onPlaceSelect: (location: Location) => void;
}

export default function LocationSearch({ onPlaceSelect }: LocationSearchProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const places = useMapsLibrary("places");

  useEffect(() => {
    if (!places || !inputRef.current) return;

    const autocomplete = new places.Autocomplete(inputRef.current, {
      fields: ["name", "geometry"],
    });

    autocomplete.addListener("place_changed", () => {
      const place = autocomplete.getPlace();
      if (!place.geometry?.location) return;

      const newLocation: Location = {
        name: place.name!,
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng(),
      };
      onPlaceSelect(newLocation);

      // Clear the input
      if(inputRef.current) {
        inputRef.current.value = "";
      }
    });
  }, [places, onPlaceSelect]);

  return (
    <input
      ref={inputRef}
      type="text"
      placeholder="Search for a location..."
      className="w-full p-2 border border-gray-300 rounded text-base"
    />
  );
}
