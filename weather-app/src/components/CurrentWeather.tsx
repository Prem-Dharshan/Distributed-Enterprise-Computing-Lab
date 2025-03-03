import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

const API_URL = "http://api.weatherstack.com/current";
const API_KEY = import.meta.env.VITE_WEATHERSTACK_API_KEY;

const fetchWeather = async (city: string) => {
  if (!city) return null;
  const { data } = await axios.get(API_URL, {
    params: { access_key: API_KEY, query: city },
  });
  return data;
};

const CurrentWeather = () => {
  const [city, setCity] = useState("New York");
  const { data, error, isLoading, refetch } = useQuery({
    queryKey: ["weather", city],
    queryFn: () => fetchWeather(city),
    enabled: false, // Only fetch on user action
  });

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <Card className="w-full max-w-md p-4 shadow-lg rounded-2xl">
        <CardHeader>
          <CardTitle className="text-xl font-semibold">Weather Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2 mb-4">
            <Input
              placeholder="Enter city name"
              value={city}
              onChange={(e) => setCity(e.target.value)}
            />
            <Button onClick={() => refetch()}>Search</Button>
          </div>

          {isLoading && <Skeleton className="h-20 w-full" />}
          {error && <p className="text-red-500">Error fetching data</p>}
          
          {data && data.current && (
            <div className="text-center">
              <h2 className="text-2xl font-bold">{data.location.name}, {data.location.country}</h2>
              <img 
                src={data.current.weather_icons[0]} 
                alt={data.current.weather_descriptions[0]} 
                className="mx-auto my-2"
              />
              <p className="text-lg">{data.current.weather_descriptions[0]}</p>
              <p className="text-4xl font-bold">{data.current.temperature}°C</p>
              <p>Feels like: {data.current.feelslike}°C</p>
              <p>Humidity: {data.current.humidity}%</p>
              <p>Wind: {data.current.wind_speed} km/h {data.current.wind_dir}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default CurrentWeather;
