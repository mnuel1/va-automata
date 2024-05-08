import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { MainScreen } from './screens/mainScreen'

function App() {

  return (
    <>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<MainScreen />}>
                {/* <Route index element={<Navigate replace to={"home"} />} />
                <Route path="home" element={<Home />} /> */}
                </Route>
            </Routes>
        </BrowserRouter>
          
    </>
  )
}

export default App

