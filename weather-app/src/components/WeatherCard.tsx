import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export interface WeatherData {
  location: {
    name: string;
    country: string;
    region: string;
  };
  current: {
    observation_time: string;
    temperature: number;
    weather_icons: string[];
    weather_descriptions: string[];
  };
}

interface WeatherCardProps {
  data: WeatherData;
}

const WeatherCard: React.FC<WeatherCardProps> = ({ data }) => {
  return (
    <Card className="max-w-3xl mx-auto">
      <CardHeader>
        <div className="flex items-center gap-4">
          {/* Weather Icon on the Left */}
          <img
            src={data.current.weather_icons[0]}
            alt={data.current.weather_descriptions[0]}
            className="w-12 h-12"
          />
          <div>
            <CardTitle className="text-xl font-bold">
              {data.location.name}, {data.location.country}
            </CardTitle>
            <p className="font-bold text-lg">{data.current.temperature}°C</p>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <p>
          <span className="font-semibold">Region:</span> {data.location.region}
        </p>
        <p>
          <span className="font-semibold">Observation Time:</span>{" "}
          {data.current.observation_time}
        </p>
        <p>
          <span className="font-semibold">Weather:</span>{" "}
          {data.current.weather_descriptions.join(", ")}
        </p>
      </CardContent>
    </Card>
  );
};

export default WeatherCard;
