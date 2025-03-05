import { FC } from "react";
import { motion } from "framer-motion";
import Random from "../components/Random";
import Veggie from "../components/Veggie";

const Home: FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Random />
      <Veggie />
    </motion.div>
  );
};

export default Home;
