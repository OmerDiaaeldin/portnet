import { useEffect, useState } from "react";
import InvoiceForm from "./InvoiceForm"

export default function Invoice() {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    return (<>
        <div className="p-8 bg-blue">
            <button
                onClick={openModal}
                className="px-4 py-2 bg-red-50 text-gray-800 rounded-md hover:bg-blue-700"
            >
                Create Invoice
            </button>

            {/* Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-lg shadow-lg w-full max-w-4xl">
                        <div className="flex justify-between items-center p-4 border-b">
                            <h2 className="text-xl font-bold">Invoice Form</h2>
                            <button
                                onClick={closeModal}
                                className="text-gray-900 hover:text-gray-700"
                            >
                                &times;
                            </button>
                        </div>
                        <div className="p-4">
                            <InvoiceForm onClose={closeModal} />
                        </div>
                    </div>
                </div>
            )}
        </div>
    </>
    );
}