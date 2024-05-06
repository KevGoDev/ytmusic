import { Outlet } from "react-router-dom";
import MainLayout from "../pages/main-layout";
import IngredientsPage from "../pages/dashboard/ingredients";

export const dashboardRoutes = [
  {
    element: (
      <MainLayout>
        <Outlet />
      </MainLayout>
    ),
    children: [
      { path: "ingredients", element: <IngredientsPage /> },
    ],
  },
];
