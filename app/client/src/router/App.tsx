import { createBrowserRouter } from "react-router-dom";
import  Chat from "@pages/chat/Chat";
import Layout from "../layout/Layout";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    
  },
  {
    path: "/chat",
    element: <Chat />
  }
]);
