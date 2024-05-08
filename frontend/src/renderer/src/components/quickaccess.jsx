
const QuickAccess = ({title, description}) => {

    return (
        <div className="flex flex-col gap-2 bg-[#1E1E1E] rounded-md p-4 min-w-[350px] w-[450px]
        hover:bg-[#1E1E2E] cursor-pointer">
            <h1 className="text-white text-lg">{title}</h1>
            <h2 className="text-white text-sm opacity-50">{description}</h2>
        </div>
    )

}

export default QuickAccess