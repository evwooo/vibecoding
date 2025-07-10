# Travel Map (Next.js Version)

This is a web application that allows you to search for locations, mark them on a map, and save them to a list in your browser, built with Next.js and Google Maps.

## How to Set Up

1.  **Install Dependencies:**
    *   If you haven't already, open your terminal in the project directory and run:
        ```bash
        npm install
        ```

2.  **Set Up Your Google Maps API Key:**
    *   Follow the instructions in the original README to get a Google Maps API Key. Make sure you have enabled both the **"Maps JavaScript API"** and the **"Places API"**.
    *   In the root of the project, create a new file named `.env.local`.
    *   Add your API key to this file like so:
        ```
        NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=YOUR_API_KEY_HERE
        ```
    *   Replace `YOUR_API_KEY_HERE` with your actual key.

3.  **Run the Development Server:**
    *   Start the application with the following command:
        ```bash
        npm run dev
        ```
    *   Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

## How It Works

*   **Search:** Use the search bar to find any location. The app uses the Google Places API for autocomplete suggestions.
*   **Save:** When you select a location from the search results, it is automatically added to your "Visited Locations" list and a marker is placed on the map.
*   **View:** Click on any location in the list to pan the map to its marker.
*   **Delete:** Hover over a location in the list and click the "Delete" button to remove it.
*   **Storage:** Your list of locations is saved in your browser's `localStorage`, so it will be there the next time you open the app.