"use client";

import { useRef, useEffect, useState } from "react";
import { useMapsLibrary } from "@vis.gl/react-google-maps";
import type { Location } from "@/app/page";
import { LOCATION_CATEGORIES } from "@/app/page";

interface LocationSearchProps {
  onPlaceSelect: (location: Omit<Location, 'id'>) => void;
}

export default function LocationSearch({ onPlaceSelect }: LocationSearchProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [selectedPlace, setSelectedPlace] = useState<google.maps.places.PlaceResult | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [locationData, setLocationData] = useState({
    category: 'Other',
    notes: '',
    dateVisited: new Date().toISOString().split('T')[0],
    rating: 3
  });
  const places = useMapsLibrary("places");

  useEffect(() => {
    if (!places || !inputRef.current) return;

    const autocomplete = new places.Autocomplete(inputRef.current, {
      fields: ["name", "geometry", "formatted_address", "types"],
    });

    autocomplete.addListener("place_changed", () => {
      const place = autocomplete.getPlace();
      if (!place.geometry?.location) return;

      setSelectedPlace(place);
      setShowModal(true);

      // Clear the input
      if(inputRef.current) {
        inputRef.current.value = "";
      }
    });
  }, [places]);

  const handleSubmit = () => {
    if (!selectedPlace?.geometry?.location) return;

    const newLocation: Omit<Location, 'id'> = {
      name: selectedPlace.name!,
      lat: selectedPlace.geometry.location.lat(),
      lng: selectedPlace.geometry.location.lng(),
      category: locationData.category,
      notes: locationData.notes,
      dateVisited: locationData.dateVisited,
      rating: locationData.rating
    };

    onPlaceSelect(newLocation);
    setShowModal(false);
    setSelectedPlace(null);
    setLocationData({
      category: 'Other',
      notes: '',
      dateVisited: new Date().toISOString().split('T')[0],
      rating: 3
    });
  };

  const handleCancel = () => {
    setShowModal(false);
    setSelectedPlace(null);
    setLocationData({
      category: 'Other',
      notes: '',
      dateVisited: new Date().toISOString().split('T')[0],
      rating: 3
    });
  };

  const renderStars = (rating: number, onRatingChange: (rating: number) => void) => {
    return (
      <div className="flex items-center space-x-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => onRatingChange(star)}
            className={`text-lg ${
              star <= rating ? 'text-yellow-400' : 'text-gray-300'
            } hover:text-yellow-500 cursor-pointer transition-colors`}
            type="button"
          >
            ★
          </button>
        ))}
      </div>
    );
  };

  return (
    <>
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          placeholder="Search for a location..."
          className="w-full p-3 border border-gray-300 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold mb-4">Add Location Details</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Location: {selectedPlace?.name}
                </label>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <select
                  value={locationData.category}
                  onChange={(e) => setLocationData({...locationData, category: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {LOCATION_CATEGORIES.map(category => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date Visited
                </label>
                <input
                  type="date"
                  value={locationData.dateVisited}
                  onChange={(e) => setLocationData({...locationData, dateVisited: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Rating
                </label>
                {renderStars(locationData.rating, (rating) => setLocationData({...locationData, rating}))}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notes
                </label>
                <textarea
                  value={locationData.notes}
                  onChange={(e) => setLocationData({...locationData, notes: e.target.value})}
                  placeholder="Add any notes about this location..."
                  className="w-full p-2 border border-gray-300 rounded-lg h-24 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={handleCancel}
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSubmit}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Add Location
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
