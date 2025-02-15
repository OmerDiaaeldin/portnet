import React from "react";

type CsvData = {
  "Exporter Details": string;
  "Country of Origin": string;
  "Vessel Name": string;
  "Voyage No": string;
  "Port of Loading (POL)": string;
  "Port of Discharge (POD)": string;
  "Final Destination (Country)": string;
  "Product Code": string;
  "Description of Goods": string;
  "HS Code": string;
  "Unit Quantity": string;
  "Unit Type": string;
  "Price (per unit)": string;
  Currency: string;
};

type TableProps = {
  data: CsvData[];
};

const Table: React.FC<TableProps> = ({ data }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Exporter Details
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Country of Origin
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Vessel Name
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Voyage No
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Port of Loading (POL)
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Port of Discharge (POD)
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Final Destination (Country)
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Product Code
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Description of Goods
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              HS Code
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Unit Quantity
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Unit Type
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Price (per unit)
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Currency
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {data.map((row, index) => (
            <tr key={index} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Exporter Details"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Country of Origin"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Vessel Name"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Voyage No"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Port of Loading (POL)"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Port of Discharge (POD)"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Final Destination (Country)"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Product Code"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Description of Goods"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["HS Code"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Unit Quantity"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Unit Type"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Price (per unit)"]}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {row["Currency"]}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;