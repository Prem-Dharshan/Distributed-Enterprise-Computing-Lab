import axios from "axios";

const CURRENT_API_URL = "http://api.weatherstack.com/current";
const API_KEY = import.meta.env.VITE_WEATHERSTACK_API_KEY;

export const fetchCurrentWeather = async (city: string) => {
  try {
    const response = await axios.get(CURRENT_API_URL, {
      params: {
        access_key: API_KEY,
        query: city,
      },
    });

    console.log(response);

    // Check for valid response data
    if (!response.data || !response.data.current) {
      throw new Error("City not found");
    }

    return response.data;  // Return the successful response data
  } catch (error: unknown) {
    // Typecast error to AxiosError or any error object for better handling
    if (axios.isAxiosError(error)) {
      // Handle Axios-specific error
      throw new Error(error.response?.data?.error?.info || "Error fetching weather data");
    } else {
      // Handle general errors
      throw new Error("An unexpected error occurred");
    }
  }
};
