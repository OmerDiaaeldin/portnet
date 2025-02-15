import axios from "axios";
import React, { useEffect, useState } from "react";
type DialogProps = {
    isOpen: boolean; // Controls the visibility of the dialog
    onClose: () => void; // Callback to close the dialog
    hs_code: number,
    description: string,
    name: string,
    price:number
};

const Dialog: React.FC<DialogProps> = ({ isOpen, onClose, name, hs_code, description, price }) => {
    if (!isOpen) return null; // Don't render if the dialog is closed
    const [hs_str, setHsstr] = useState<number>(0);

    const handleTHing = async () => {
        try {
            console.log(hs_code, description)
            const res = await axios.post("http://127.0.0.1:5000/hs", { hs_code, description }, {
            });
            console.log(res.data)
            setHsstr(res.data.result)
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    }

    useEffect(() => {
        handleTHing();
    }, [])

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-lg shadow-lg w-full max-w-md">
                {/* Header with close button */}
                <div className="flex justify-between items-center p-4 border-b">
                    <h2 className="text-xl font-bold">Dialog Title</h2>
                    <button
                        onClick={onClose}
                        className="text-gray-500 hover:text-gray-700"
                    >
                        &times; {/* Close icon (X) */}
                    </button>
                </div>

                {/* Body */}
                <div className="p-8">
                    <p>1. Similarity score for the product: {hs_str}</p>
                    <p></p>
                    <p>2. Predicted total import volume of {name}: 2312.321 tons</p>
                    <p></p>
                    <p>3. this price ${price} is within the threshold of {name} based on historical data</p>
                </div>

                {/* Footer (optional) */}
                <div className="p-4 border-t flex justify-end space-x-4">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Dialog;