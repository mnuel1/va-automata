
import Intro from "../components/intro"
import QuickAccess from "../components/quickaccess"

const Home = () => {

    return (
        <>
            <div>

            </div>   
            <div className="w-full flex flex-col justify-center items-center">                            
                <Intro/>

                <div className="grid grid-cols-1 xl:grid-cols-2 mt-12 gap-2">
                    {/* remove 2 if mobile view */}
                    <QuickAccess title={"Sample title"} description={"Sample description"}/>
                    <QuickAccess title={"Sample title"} description={"Sample description"}/>
                    <QuickAccess title={"Sample title"} description={"Sample description"}/>
                    <QuickAccess title={"Sample title"} description={"Sample description"}/>
            
                </div>
                

            </div>     
        
        </>
       
    )


}

export default Home