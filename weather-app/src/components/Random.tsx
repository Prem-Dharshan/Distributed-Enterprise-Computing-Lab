import { useEffect } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Skeleton } from "@/components/ui/skeleton";
import { Carousel } from "./ui/carousel";

const fetchRandomRecipes = async () => {
  const apiKey = import.meta.env.VITE_SPOONACULAR_API_KEY;
  const resp = await fetch(
    `https://api.spoonacular.com/recipes/random?apiKey=${apiKey}&number=10`
  );
  const data = await resp.json();
  return data.recipes;
};

const Random: React.FC = () => {
  const { data: random, isLoading, error, refetch } = useQuery({
    queryKey: ["randomRecipes"],
    queryFn: fetchRandomRecipes,
    staleTime: 1000 * 60 * 10, // Cache for 10 minutes
  });

  useEffect(() => {
    refetch();
  }, [refetch]);

  if (isLoading) {
    return (
      <div className="flex justify-center gap-4">
        {[...Array(4)].map((_, i) => (
          <Skeleton key={i} className="w-64 h-64 rounded-2xl" />
        ))}
      </div>
    );
  }

  if (error) {
    return <p className="text-red-500 text-center">Failed to load recipes.</p>;
  }

  return (
    <div className="my-8">
      <h3 className="text-xl font-bold text-center mb-6">Random Picks</h3>
      <Carousel
        slidesToShow={4}
        slidesToScroll={1}
        breakpoints={{
          1024: { slidesToShow: 3 },
          767: { slidesToShow: 2 },
          640: { slidesToShow: 1 },
        }}
        className="overflow-hidden"
      >
        {random?.map(({ title, id, image }) => (
          <div key={id} className="relative w-64 h-64 overflow-hidden rounded-2xl shadow-lg">
            <Link to={`/recipe/${id}`}>
              <p className="absolute bottom-0 left-0 w-full bg-black/50 text-white text-center py-2 font-semibold">
                {title}
              </p>
              <img
                src={image}
                alt={title}
                className="w-full h-full object-cover rounded-2xl"
              />
            </Link>
          </div>
        ))}
      </Carousel>
    </div>
  );
};

export default Random;
