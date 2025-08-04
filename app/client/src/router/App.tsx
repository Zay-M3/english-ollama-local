import { createBrowserRouter } from "react-router-dom";
import  Chat from "@pages/chat/Chat";
import Layout from "../layout/Layout";
import Home from "../layout/home/Home";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: "chat", element: <Chat /> }
    ]
    
  },
]);
