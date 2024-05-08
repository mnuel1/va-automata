
import Logo from "./logo"

const Sidebar = () => {

    return (
        <>
            <div className="flex flex-col min-w-[300px] border-r border-white border-opacity-10 p-6">

                <div className="flex  items-center mt-5 px-2 py-1">
                    <Logo />
                </div>

                <div className="flex flex-col flex-grow gap-2 mt-12">
                    <div className="w-full h-[60px] bg-white"></div>
                    <div className="w-full h-[60px] bg-white"></div>
                    <div className="w-full h-[60px] bg-white"></div>
                    

                </div>

                <div className="flex items-center justify-center ">
                    <span className="text-xs text-gray-400 opacity-40">© 2024 BSCSNS - 3AB™. All rights reserved.</span>
                </div>

            </div>

        </>
    )

}

export default Sidebar