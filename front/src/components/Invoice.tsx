import { useEffect, useState } from "react";
import InvoiceForm from "./InvoiceForm"
import Table from "./Table";
import Papa from "papaparse";

export default function Invoice() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [invoiceData, setInvoiceData] = useState([]);

    useEffect(() => {
        // Fetch the CSV file
        fetch("/home/odaio/dev/portnet/back/data/Generated_Invoices.csv")
            .then((response) => {
                console.log(response);
                return response.text()})
            .then((csvText) => {
                console.log(csvText)
                Papa.parse(csvText, {
                    header: true, // Use the first row as headers
                    dynamicTyping: true, // Automatically convert numeric values
                    complete: (result: any) => {
                        setInvoiceData(result.data); // Set the parsed data
                    },
                });
            });
    }, []);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    return (<>
        <Table data={invoiceData} />
        <div className="p-8 bg-blue">
            <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
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