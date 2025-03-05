import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { Link, useParams } from "react-router-dom";

// API call function using Axios
const fetchCuisines = async (cuisine: string) => {
    const apiKey = import.meta.env.VITE_SPOONACULAR_API_KEY;
  const resp = await axios.get(
    `https://api.spoonacular.com/recipes/complexSearch?apiKey=${apiKey}&cuisine=${cuisine}`
  );
  return resp.data.results;
};

const Cuisines: React.FC = () => {
  const { type } = useParams<{ type: string }>();

  // TanStack Query hook to fetch cuisines data
  const { data: cuisines, isLoading } = useQuery(
    {
      queryKey: ["cuisines", type],
      queryFn: () => fetchCuisines(type!),
      enabled: !!type,
      staleTime: 1000 * 60 * 5,
    } // Cache for 5 minutes
  );

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="my-8">
      <h3 className="text-2xl font-bold text-center mb-6">Cuisines: {type}</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
        {cuisines?.map(({ id, title, image }) => (
          <div
            key={id}
            className="relative rounded-2xl shadow-lg overflow-hidden"
          >
            <Link to={`/recipe/${id}`} className="block">
              <img
                src={image}
                alt={title}
                className="w-full h-64 object-cover rounded-t-2xl"
              />
              <div className="absolute bottom-0 left-0 w-full bg-black/50 text-white text-center py-2 font-semibold">
                {title}
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Cuisines;
