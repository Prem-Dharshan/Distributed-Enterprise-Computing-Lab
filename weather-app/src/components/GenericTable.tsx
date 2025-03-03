import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

interface GenericTableProps {
  headers: string[]; // Array of table headers
  data: string[][]; // 2D array of data (each row is an array of cell values)
}

const GenericTable = ({ headers, data }: GenericTableProps) => {
  return (
    <Table className="w-full">
      <TableCaption>A list of weather metrics.</TableCaption>
      <TableHeader>
        <TableRow>
          {headers.map((header, index) => (
            <TableHead key={index}>{header}</TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((row, rowIndex) => (
          <TableRow key={rowIndex}>
            {row.map((cell, cellIndex) => (
              <TableCell key={cellIndex}>{cell}</TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default GenericTable;
