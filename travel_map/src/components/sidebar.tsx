"use client";

import { useState, useRef } from "react";
import type { Location } from "@/app/page";
import { LOCATION_CATEGORIES } from "@/app/page";
import LocationSearch from "./location-search";

interface SidebarProps {
  locations: Location[];
  onAddLocation: (location: Omit<Location, 'id'>) => void;
  onUpdateLocation: (id: string, updates: Partial<Location>) => void;
  onDeleteLocation: (id: string) => void;
  onSelectLocation: (location: Location) => void;
  onExportLocations: () => void;
  onImportLocations: (file: File) => void;
}

type SortOption = 'name' | 'date' | 'rating' | 'category';

export default function Sidebar({
  locations,
  onAddLocation,
  onUpdateLocation,
  onDeleteLocation,
  onSelectLocation,
  onExportLocations,
  onImportLocations,
}: SidebarProps) {
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [sortBy, setSortBy] = useState<SortOption>('date');
  const [searchQuery, setSearchQuery] = useState('');
  const [editingLocation, setEditingLocation] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const filteredAndSortedLocations = locations
    .filter(location => {
      const matchesCategory = filterCategory === 'all' || location.category === filterCategory;
      const matchesSearch = location.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           location.notes.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'date':
          return new Date(b.dateVisited).getTime() - new Date(a.dateVisited).getTime();
        case 'rating':
          return b.rating - a.rating;
        case 'category':
          return a.category.localeCompare(b.category);
        default:
          return 0;
      }
    });

  const handleFileImport = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onImportLocations(file);
      event.target.value = '';
    }
  };

  const handleLocationEdit = (location: Location, field: keyof Location, value: string | number) => {
    onUpdateLocation(location.id, { [field]: value });
  };

  const renderStars = (rating: number, editable: boolean = false, onRatingChange?: (rating: number) => void) => {
    return (
      <div className="flex items-center space-x-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => editable && onRatingChange?.(star)}
            className={`text-sm ${
              star <= rating ? 'text-yellow-400' : 'text-gray-300'
            } ${editable ? 'hover:text-yellow-500 cursor-pointer' : ''}`}
            disabled={!editable}
          >
            ★
          </button>
        ))}
      </div>
    );
  };

  return (
    <div className="w-[400px] bg-white border-r border-gray-200 flex flex-col shadow-xl">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <h1 className="text-2xl font-bold">Travel Map</h1>
        <p className="text-blue-100 mt-1">{locations.length} locations visited</p>
      </div>

      {/* Search and Add Location */}
      <div className="p-4 border-b border-gray-200 bg-gray-50">
        <LocationSearch onPlaceSelect={onAddLocation} />
      </div>

      {/* Controls */}
      <div className="p-4 border-b border-gray-200 bg-gray-50 space-y-3">
        {/* Search Filter */}
        <div>
          <input
            type="text"
            placeholder="Search locations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Category Filter and Sort */}
        <div className="flex space-x-2">
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="flex-1 p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Categories</option>
            {LOCATION_CATEGORIES.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortOption)}
            className="flex-1 p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="date">Sort by Date</option>
            <option value="name">Sort by Name</option>
            <option value="rating">Sort by Rating</option>
            <option value="category">Sort by Category</option>
          </select>
        </div>

        {/* Import/Export */}
        <div className="flex space-x-2">
          <button
            onClick={onExportLocations}
            className="flex-1 bg-green-500 text-white px-3 py-2 rounded-lg text-sm hover:bg-green-600 transition-colors"
          >
            Export
          </button>
          <button
            onClick={() => fileInputRef.current?.click()}
            className="flex-1 bg-blue-500 text-white px-3 py-2 rounded-lg text-sm hover:bg-blue-600 transition-colors"
          >
            Import
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".json"
            onChange={handleFileImport}
            className="hidden"
          />
        </div>
      </div>

      {/* Location List */}
      <div className="flex-1 overflow-y-auto">
        {filteredAndSortedLocations.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            {locations.length === 0 ? (
              <div>
                <p className="text-lg font-medium">No locations yet</p>
                <p className="text-sm mt-2">Search for a location above to get started!</p>
              </div>
            ) : (
              <p>No locations match your current filters</p>
            )}
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {filteredAndSortedLocations.map((location) => (
              <li key={location.id} className="p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-2">
                      <button
                        onClick={() => onSelectLocation(location)}
                        className="text-left font-medium text-gray-900 hover:text-blue-600 transition-colors truncate"
                      >
                        {location.name}
                      </button>
                      <button
                        onClick={() => setEditingLocation(editingLocation === location.id ? null : location.id)}
                        className="text-gray-400 hover:text-gray-600 p-1"
                      >
                        {editingLocation === location.id ? '✓' : '✎'}
                      </button>
                    </div>

                    <div className="space-y-2">
                      <div className="flex items-center space-x-2 text-sm text-gray-600">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                          {location.category}
                        </span>
                        <span>•</span>
                        <span>{location.dateVisited}</span>
                      </div>

                      {editingLocation === location.id ? (
                        <div className="space-y-2">
                          <select
                            value={location.category}
                            onChange={(e) => handleLocationEdit(location, 'category', e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded text-sm"
                          >
                            {LOCATION_CATEGORIES.map(category => (
                              <option key={category} value={category}>{category}</option>
                            ))}
                          </select>
                          <input
                            type="date"
                            value={location.dateVisited}
                            onChange={(e) => handleLocationEdit(location, 'dateVisited', e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded text-sm"
                          />
                          <textarea
                            value={location.notes}
                            onChange={(e) => handleLocationEdit(location, 'notes', e.target.value)}
                            placeholder="Add notes..."
                            className="w-full p-2 border border-gray-300 rounded text-sm h-20 resize-none"
                          />
                          <div className="flex items-center space-x-2">
                            <span className="text-sm text-gray-600">Rating:</span>
                            {renderStars(location.rating, true, (rating) => handleLocationEdit(location, 'rating', rating))}
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-1">
                          {location.notes && (
                            <p className="text-sm text-gray-600 line-clamp-2">{location.notes}</p>
                          )}
                          {renderStars(location.rating)}
                        </div>
                      )}
                    </div>
                  </div>

                  <button
                    onClick={() => onDeleteLocation(location.id)}
                    className="ml-3 text-red-500 hover:text-red-700 p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    🗑️
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
