"use client";

import type { Location } from "@/app/page";
import LocationSearch from "./location-search";

interface SidebarProps {
  locations: Location[];
  onAddLocation: (location: Location) => void;
  onDeleteLocation: (index: number) => void;
  onSelectLocation: (location: Location) => void;
}

export default function Sidebar({
  locations,
  onAddLocation,
  onDeleteLocation,
  onSelectLocation,
}: SidebarProps) {
  return (
    <div className="w-[350px] bg-gray-100 border-r border-gray-300 flex flex-col p-5 shadow-lg z-10">
      <h1 className="text-2xl font-bold mt-0 text-gray-800">Visited Locations</h1>
      <div className="my-5">
        <LocationSearch onPlaceSelect={onAddLocation} />
      </div>
      <ul className="list-none p-0 m-0 overflow-y-auto flex-grow">
        {locations.map((location, index) => (
          <li
            key={index}
            className="p-4 border-b border-gray-200 cursor-pointer flex justify-between items-center group hover:bg-gray-200 transition-colors"
            onClick={() => onSelectLocation(location)}
          >
            <span>{location.name}</span>
            <button
              className="bg-red-500 text-white border-none py-1 px-2 rounded cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity"
              onClick={(e) => {
                e.stopPropagation(); // Prevent li's onClick from firing
                onDeleteLocation(index);
              }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
