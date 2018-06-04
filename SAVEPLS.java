package com.infor.coleman.backend.execution.spark_emr.executor;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Consumer;

import org.apache.spark.sql.DataFrameReader;
import org.apache.spark.sql.DataFrameWriter;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.junit.Test;

import com.crealytics.spark.excel.ExcelRelation;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.JsonNodeType;
import com.infor.coleman.backend.execution.spark_emr.SchemaUtil;
import com.infor.colemanui.backend.metadata.schema.Schema;
import com.infor.colemanui.backend.model.DatasetSchemaDO;
import com.infor.colemanui.backend.serialization.ObjectMappers;


@SuppressWarnings("unused")
public class LocalSparkTest {
	public String readStringFromFile(String filePath) throws IOException {
	    String fileContent = new String(Files.readAllBytes(Paths.get(new File(filePath).getAbsolutePath())));
	    return fileContent;
	}
	
	@Test
	public void testLocal() throws JsonProcessingException, IOException {
		String relativePath = "src/test/java/com/infor/coleman/backend/execution/spark_emr/executor/sampleData/";
		String readArgsStr = readStringFromFile(relativePath + "readArgs.json");
		String writeArgsStr = readStringFromFile(relativePath + "writeArgs.json");
		String schemaStr = readStringFromFile(relativePath + "schema.json");

		// Overwrite paths since json cannot represent absolute paths
		String ABSOLUTE_DIR = Paths.get("").toAbsolutePath().toString().replace("\\", "/") + "/src/test/java/com/infor/coleman/backend/execution/spark_emr/executor/sampleData/";
		readArgsStr = readArgsStr.replaceAll("<ABSOLUTE_DIR>", ABSOLUTE_DIR);
		writeArgsStr = writeArgsStr.replaceAll("<ABSOLUTE_DIR>", ABSOLUTE_DIR);
		
		System.out.println("readArgs json: " + readArgsStr);
		System.out.println("writeArgs json: " + writeArgsStr);
		System.out.println("schema json: " + schemaStr);

		ObjectMapper mapper = new ObjectMapper();
		JsonNode readArgs = mapper.readTree(readArgsStr);
		JsonNode writeArgs = mapper.readTree(writeArgsStr);
		DatasetSchemaDO datasetSchema = new DatasetSchemaDO(UUID.randomUUID().toString(), ObjectMappers.DYNAMODB.reader(Schema.class).readValue(schemaStr));
		loadDatasetData(readArgs, writeArgs, datasetSchema.getSchemaPropeties());
	}
	
	static Consumer<String> LOG = (s) -> System.out.println(s);
	private SparkSession getSparkSession() { return SparkSession.builder().master("local[2]").getOrCreate(); }
	
	public void checkRequiredFields(List<String> requiredFields, List<String> fields, String missingMessage) {
		requiredFields.removeAll(fields);
		if (!requiredFields.isEmpty()) {
			throw new IllegalArgumentException(missingMessage + requiredFields);
		}
	}
	
	public LoadableOption<?> loadOptions(LoadableOption<?> loader, List<String> fields, JsonNode json) {
		for (String field : fields) {
			loader = (LoadableOption<?>) loader.genericOption(field, json.get(field));
		}
		return loader;
	}
	
	public LoadableOption<?> loadFormat(LoadableOption<?> loader, String format, JsonNode json) {
		List<String> delimitedFormats = Arrays.asList("csv", "tsv", "dsv");
		List<String> excelFormats = Arrays.asList("xls", "xlsx");
		if (delimitedFormats.contains(format)) {
			loader = (LoadableOption<?>) loader.format("csv");
		} else if (excelFormats.contains(format)) {
			loader = (LoadableOption<?>) loader.format("com.crealytics.spark.excel");
			loader = (LoadableOption<?>) loader.option("useHeader", json.get("header").asBoolean(false));
		} else {
			loader = (LoadableOption<?>) loader.format(format);
		}
		return loader;
	}

	public StructType parseSchemaMetadata(Map<String, Schema> schemaMetadata) { // TODO: if inferSchema but have spaces -> Attribute name "Employee ID" contains invalid character(s) among " ,;{}()\n\t=". Please use alias to rename it.;
		if (schemaMetadata == null) {
			return null;
		}
		StructType sparkSchema = new StructType();
		List<StructField> fields = new ArrayList<>();
		for (Map.Entry<String, Schema> entry : schemaMetadata.entrySet()) {
			StructField field = DataTypes.createStructField(entry.getKey(), SchemaUtil.translateDataType(entry.getValue()), false);
			fields.add(field);
		}
		sparkSchema = DataTypes.createStructType(fields);
		return sparkSchema;
	}
	
	public Dataset<Row> invalidColumnRename(Dataset<Row> df) { // TODO CONTINUE HERE
		for (String colName : df.columns()) {
			df = df.withColumnRenamed(colName, colName.replaceAll("[ ,;{}()\n\t=]", "_"));
		}
		return df;
	}

	public void loadDatasetData(JsonNode readArgsJson, JsonNode writeArgsJson, Map<String, Schema> schemaMetadata) {
		int maxShow = 50;
		try {
			// Get Spark Session
			SparkSession spark = getSparkSession();

			// Check for the required read arguments and "guard" arguments to be referred to
			List<String> requiredReadFields = new ArrayList<String>(Arrays.asList("path", "format"));
			List<String> readFields = new ArrayList<>();
			readArgsJson.fieldNames().forEachRemaining(readFields::add);
			checkRequiredFields(requiredReadFields, readFields, "Unable to find required read arguments: ");
			String readFormat = readArgsJson.get("format").asText();

			// Initialize read arguments
			DataFrameReader dfre = new DataFrameReaderExtension(spark);
			dfre = (DataFrameReader) loadOptions((LoadableOption<?>) dfre, readFields, readArgsJson);
			// Load format and format-specific options
			dfre = (DataFrameReader) loadFormat((LoadableOption<?>) dfre, readFormat, readArgsJson);
			// Load schema
			StructType schema = parseSchemaMetadata(schemaMetadata);
			dfre = (schema == null) ? dfre.option("inferSchema", true) : dfre.schema(schema);
			// Load Dataset
			Dataset<Row> df = dfre.load();
			
			// Replace invalid characters in column names
			df = invalidColumnRename(df);

			// Check for the required write arguments and "guard" arguments to be referred to
			List<String> requiredWriteFields = new ArrayList<String>(Arrays.asList("path", "format", "mode"));
			List<String> writeFields = new ArrayList<String>();
			writeArgsJson.fieldNames().forEachRemaining(writeFields::add);
			checkRequiredFields(requiredWriteFields, writeFields, "Unable to find required write arguments: ");
			String writeFormat = writeArgsJson.get("format").asText();
			String writeMode = writeArgsJson.get("mode").asText();
			
			// Initialize write arguments
			DataFrameWriterExtension dfwe = new DataFrameWriterExtension(df);
			dfwe = (DataFrameWriterExtension) loadOptions((LoadableOption<?>) dfwe, writeFields, writeArgsJson);
			// Load format and format-specific options
			dfwe = (DataFrameWriterExtension) loadFormat((LoadableOption<?>) dfwe, writeFormat, writeArgsJson);
			// Load saveMode
			dfwe = dfwe.mode(writeMode);
			// Save converted DataFrame
			dfwe.save();

			LOG.accept(String.format("========== (Loaded DataFrame) ============"));
			df.show(maxShow);
			LOG.accept(String.format("========== (Utilized Schema: %b) ============", (schema != null)));
			df.printSchema();
			LOG.accept(String.format("========== (Written DataFrame) ============"));
			spark.read().format("parquet").load(writeArgsJson.get("path").asText()).show(maxShow);
		} catch (Exception e) {
			LOG.accept(e.toString());
			e.printStackTrace();
		}
	}

	interface LoadableOption<T> {
		T option(String key, String s);
		T option(String key, boolean b);
		T option(String key, double d);
		T format(String format);

		@SuppressWarnings("unchecked")
		default T genericOption(String key, Object obj) {
			if (obj instanceof JsonNode) {
				JsonNode node = (JsonNode) obj;
				if (node.getNodeType() == JsonNodeType.STRING) {
					return option(key, node.asText());
				} else if (node.getNodeType() == JsonNodeType.BOOLEAN) {
					return option(key, node.asBoolean());
				} else if (node.getNodeType() == JsonNodeType.NUMBER) {
					return option(key, node.asDouble());
				}
			} else {
				if (obj.getClass() == String.class) {
					return option(key, (String) obj);
				} else if (obj.getClass() == Boolean.class) {
					return option(key, (boolean) obj);
				} else if (Number.class.isAssignableFrom(obj.getClass())) {
					return option(key, ((Number) obj).doubleValue());
				}
			}
			LOG.accept("Ignoring unsupported type from parameter: " + key);
			return (T) this;
		}
	}

	class DataFrameReaderExtension extends DataFrameReader implements LoadableOption<DataFrameReader> {
		public DataFrameReaderExtension(SparkSession sparkSession) {
			super(sparkSession);
		}
	}

	// Cannot extend final class DataFrameWriter
	class DataFrameWriterExtension implements LoadableOption<DataFrameWriterExtension> {
		private DataFrameWriter<Row> dfw;

		public DataFrameWriterExtension(Dataset<Row> ds) {
			dfw = ds.write();
		}

		public DataFrameWriterExtension format(String format) {
			dfw = dfw.format(format);
			return this;
		}

		public DataFrameWriterExtension mode(String mode) {
			dfw = dfw.mode(mode);
			return this;
		}

		public void save() {
			dfw.save();
		}

		public DataFrameWriterExtension option(String key, String s) {
			dfw = dfw.option(key, s);
			return this;
		}

		public DataFrameWriterExtension option(String key, boolean b) {
			dfw = dfw.option(key, b);
			return this;
		}

		public DataFrameWriterExtension option(String key, double d) {
			dfw = dfw.option(key, d);
			return this;
		}
	}
}
