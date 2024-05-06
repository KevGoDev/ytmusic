import { Navigate, useRoutes } from "react-router-dom";
import HomePage from "../pages/home";
import { errorRoutes } from "./error";
import MainLayout from "../pages/main-layout";


export default function Router() {
  return useRoutes([
    // Home
    {
      path: "/",
      element: <MainLayout><HomePage /></MainLayout>,
    },

    // Error(500,404, etc) handling
    ...errorRoutes,
    { path: "*", element: <Navigate to="/404" replace /> },
  ]);
}
