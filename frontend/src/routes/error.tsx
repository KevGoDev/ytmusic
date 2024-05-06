import { Outlet } from "react-router-dom";
import MainLayout from "../pages/main-layout";
import Page404 from "../pages/errors/404";

export const errorRoutes = [
  {
    element: (
      <MainLayout>
        <Outlet />
      </MainLayout>
    ),
    children: [],
  },
  {
    element: (
      <MainLayout>
        <Outlet />
      </MainLayout>
    ),
    children: [
      { path: "404", element: <Page404 /> },
    ],
  },
];
