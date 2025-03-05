import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { Carousel } from "./ui/carousel";

// Fetch veggies data
const fetchVeggies = async () => {
    const apiKey = import.meta.env.VITE_SPOONACULAR_API_KEY;
  const getData = localStorage.getItem("veggies");

  if (getData && getData !== "undefined") {
    return JSON.parse(getData);
  } else {
    const resp = await fetch(
      `https://api.spoonacular.com/recipes/random?apiKey=${apiKey}&tags=vegetarian&number=10`
    );
    const data = await resp.json();
    localStorage.setItem("veggies", JSON.stringify(data.recipes));
    return data.recipes;
  }
};

const Veggie: React.FC = () => {
  const { data: veggies, isLoading } = useQuery({
    queryKey: ["veggies"],
    queryFn: fetchVeggies,
    staleTime: 1000 * 60 * 10,
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="my-8">
      <h3 className="text-2xl font-bold text-center mb-6">Vegetarian Picks</h3>
      <Carousel
        slidesToShow={3}
        slidesToScroll={1}
        breakpoints={{
          767: { slidesToShow: 2 },
          640: { slidesToShow: 1 },
        }}
        className="space-x-6"
      >
        {veggies?.map(({ title, id, image }) => (
          <div
            key={id}
            className="relative w-64 h-80 overflow-hidden rounded-2xl shadow-lg"
          >
            <Link to={`/recipe/${id}`}>
              <img
                src={image}
                alt={title}
                className="w-full h-full object-cover rounded-2xl"
              />
              <div className="absolute bottom-0 left-0 w-full bg-black/50 text-white text-center py-2 font-semibold">
                {title}
              </div>
            </Link>
          </div>
        ))}
      </Carousel>
    </div>
  );
};

export default Veggie;
