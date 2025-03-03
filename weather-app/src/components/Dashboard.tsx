import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchCurrentWeather } from "@/services/dashboard";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { CloudSunRain } from "lucide-react";
import { InputWithButton } from "@/components/shared/InputWithButton";
import { Skeleton } from "@/components/ui/skeleton";
import GenericTable from "@/components/GenericTable";
import ErrorDialog from "./shared/ErrorDialog";
import WeatherCard, { WeatherData } from "./WeatherCard";

const Dashboard = () => {
  const [city, setCity] = useState("New York");
  const [showError, setShowError] = useState(false);

  const { data, isLoading, error, isError, refetch } = useQuery({
    queryKey: ["current", city],
    queryFn: () => fetchCurrentWeather(city),
    enabled: false,
  });

  // Trigger to show error dialog when an error occurs
  if (isError) {
    // Set error message and show error dialog
    const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
    return (
      <ErrorDialog
        isOpen={showError}
        onClose={setShowError}
        message={errorMessage}
      />
    );
  }

  const headers = ["Metric", "Value"];
  const weatherData = data
    ? [
        ["Wind Speed", `${data.current.wind_speed} km/h`],
        ["Wind Direction", data.current.wind_dir],
        ["Pressure", `${data.current.pressure} hPa`],
        ["Precipitation", `${data.current.precip} mm`],
        ["Humidity", `${data.current.humidity} %`],
        ["Cloud Cover", `${data.current.cloudcover} %`],
        ["Feels Like", `${data.current.feelslike} °C`],
        ["UV Index", `${data.current.uv_index}`],
        ["Visibility", `${data.current.visibility} km`],
      ]
    : [];

  return (
    <>
      <div className="mt-4 max-w-6xl w-full bg-white shadow-sm rounded-lg p-6 mx-auto flex flex-row items-center gap-4">
        {/* Avatar */}
        <Avatar>
          <AvatarFallback className="bg-gray-100 flex items-center justify-center w-10 h-10">
            <CloudSunRain className="w-6 h-6 text-gray-600" />
          </AvatarFallback>
        </Avatar>

        {/* Input with Button */}
        <InputWithButton
          btnText="Fetch"
          placeholderText="Enter the city"
          onSubmit={() => refetch()}
          onChange={setCity}
        />
      </div>

      {/* Skeleton Loader */}
      {isLoading && <Skeleton className="h-32 w-full" />}

      {/* Weather Data Display as a Card */}
      <div className="mt-6">
        {data && <WeatherCard data={data as WeatherData} />}
      </div>

      {/* Weather Metrics Table */}
      <div className="mt-6 max-w-6xl w-full mx-auto">
        {data && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Weather Metrics</h2>
            <GenericTable headers={headers} data={weatherData} />
          </div>
        )}
      </div>
    </>
  );
};

export default Dashboard;
