import  Home  from './screens/Home'
import Sidebar from './components/sidebar'

function App() {

  return (
    <>
        <div className='flex min-h-screen bg-[#121212]'>
            <Sidebar/>
            <Home/>
        </div>
        
    </>
  )
}

export default App

